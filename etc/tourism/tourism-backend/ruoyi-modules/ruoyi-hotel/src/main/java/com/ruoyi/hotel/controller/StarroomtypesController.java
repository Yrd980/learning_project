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
import com.ruoyi.hotel.domain.Starroomtypes;
import com.ruoyi.hotel.service.IStarroomtypesService;
import com.ruoyi.common.core.web.controller.BaseController;
import com.ruoyi.common.core.web.domain.AjaxResult;
import com.ruoyi.common.core.utils.poi.ExcelUtil;
import com.ruoyi.common.core.web.page.TableDataInfo;

/**
 * 星级酒店房型Controller
 * 
 * @author ningf
 * @date 2024-07-12
 */
@RestController
@RequestMapping("/starroomtypes")
public class StarroomtypesController extends BaseController
{
    @Autowired
    private IStarroomtypesService starroomtypesService;

    /**
     * 查询星级酒店房型列表
     */
    @RequiresPermissions("hotel:starroomtypes:list")
    @GetMapping("/list")
    public TableDataInfo list(Starroomtypes starroomtypes)
    {
        startPage();
        List<Starroomtypes> list = starroomtypesService.selectStarroomtypesList(starroomtypes);
        return getDataTable(list);
    }

    /**
     * 导出星级酒店房型列表
     */
    @RequiresPermissions("hotel:starroomtypes:export")
    @Log(title = "星级酒店房型", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, Starroomtypes starroomtypes)
    {
        List<Starroomtypes> list = starroomtypesService.selectStarroomtypesList(starroomtypes);
        ExcelUtil<Starroomtypes> util = new ExcelUtil<Starroomtypes>(Starroomtypes.class);
        util.exportExcel(response, list, "星级酒店房型数据");
    }

    /**
     * 获取星级酒店房型详细信息
     */
    @RequiresPermissions("hotel:starroomtypes:query")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(starroomtypesService.selectStarroomtypesById(id));
    }

    /**
     * 新增星级酒店房型
     */
    @RequiresPermissions("hotel:starroomtypes:add")
    @Log(title = "星级酒店房型", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody Starroomtypes starroomtypes)
    {
        return toAjax(starroomtypesService.insertStarroomtypes(starroomtypes));
    }

    /**
     * 修改星级酒店房型
     */
    @RequiresPermissions("hotel:starroomtypes:edit")
    @Log(title = "星级酒店房型", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody Starroomtypes starroomtypes)
    {
        return toAjax(starroomtypesService.updateStarroomtypes(starroomtypes));
    }

    /**
     * 删除星级酒店房型
     */
    @RequiresPermissions("hotel:starroomtypes:remove")
    @Log(title = "星级酒店房型", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(starroomtypesService.deleteStarroomtypesByIds(ids));
    }
}
