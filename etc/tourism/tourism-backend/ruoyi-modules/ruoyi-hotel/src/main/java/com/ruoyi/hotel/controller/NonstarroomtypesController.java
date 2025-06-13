package com.ruoyi.hotel.controller;

import java.util.List;
import java.io.IOException;
import javax.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.ruoyi.common.log.annotation.Log;
import com.ruoyi.common.log.enums.BusinessType;
import com.ruoyi.common.security.annotation.RequiresPermissions;
import com.ruoyi.hotel.domain.Nonstarroomtypes;
import com.ruoyi.hotel.service.INonstarroomtypesService;
import com.ruoyi.common.core.web.controller.BaseController;
import com.ruoyi.common.core.web.domain.AjaxResult;
import com.ruoyi.common.core.utils.poi.ExcelUtil;
import com.ruoyi.common.core.web.page.TableDataInfo;

/**
 * 非星级酒店房型Controller
 * 
 * @author ningf
 * @date 2024-07-14
 */
@RestController
@RequestMapping("/nonstarroomtypes")
public class NonstarroomtypesController extends BaseController
{
    @Autowired
    private INonstarroomtypesService nonstarroomtypesService;

    /**
     * 查询非星级酒店房型列表
     */
    @RequiresPermissions("hotel:nonstarroomtypes:list")
    @GetMapping("/list")
    public TableDataInfo list(Nonstarroomtypes nonstarroomtypes)
    {
        startPage();
        List<Nonstarroomtypes> list = nonstarroomtypesService.selectNonstarroomtypesList(nonstarroomtypes);
        return getDataTable(list);
    }

    /**
     * 导出非星级酒店房型列表
     */
    @RequiresPermissions("hotel:nonstarroomtypes:export")
    @Log(title = "非星级酒店房型", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, Nonstarroomtypes nonstarroomtypes)
    {
        List<Nonstarroomtypes> list = nonstarroomtypesService.selectNonstarroomtypesList(nonstarroomtypes);
        ExcelUtil<Nonstarroomtypes> util = new ExcelUtil<Nonstarroomtypes>(Nonstarroomtypes.class);
        util.exportExcel(response, list, "非星级酒店房型数据");
    }

    /**
     * 获取非星级酒店房型详细信息
     */
    @RequiresPermissions("hotel:nonstarroomtypes:query")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(nonstarroomtypesService.selectNonstarroomtypesById(id));
    }

    /**
     * 新增非星级酒店房型
     */
    @RequiresPermissions("hotel:nonstarroomtypes:add")
    @Log(title = "非星级酒店房型", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody Nonstarroomtypes nonstarroomtypes)
    {
        return toAjax(nonstarroomtypesService.insertNonstarroomtypes(nonstarroomtypes));
    }

    /**
     * 修改非星级酒店房型
     */
    @RequiresPermissions("hotel:nonstarroomtypes:edit")
    @Log(title = "非星级酒店房型", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody Nonstarroomtypes nonstarroomtypes)
    {
        return toAjax(nonstarroomtypesService.updateNonstarroomtypes(nonstarroomtypes));
    }

    /**
     * 删除非星级酒店房型
     */
    @RequiresPermissions("hotel:nonstarroomtypes:remove")
    @Log(title = "非星级酒店房型", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(nonstarroomtypesService.deleteNonstarroomtypesByIds(ids));
    }
}
