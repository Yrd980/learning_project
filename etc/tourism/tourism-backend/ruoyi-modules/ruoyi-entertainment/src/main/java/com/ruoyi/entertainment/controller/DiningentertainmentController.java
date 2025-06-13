package com.ruoyi.entertainment.controller;

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
import com.ruoyi.entertainment.domain.Diningentertainment;
import com.ruoyi.entertainment.service.IDiningentertainmentService;
import com.ruoyi.common.core.web.controller.BaseController;
import com.ruoyi.common.core.web.domain.AjaxResult;
import com.ruoyi.common.core.utils.poi.ExcelUtil;
import com.ruoyi.common.core.web.page.TableDataInfo;

/**
 * 餐饮娱乐信息Controller
 * 
 * @author ningf
 * @date 2024-07-08
 */
@RestController
@RequestMapping("/diningentertainment")
public class DiningentertainmentController extends BaseController
{
    @Autowired
    private IDiningentertainmentService diningentertainmentService;

    /**
     * 查询餐饮娱乐信息列表
     */
    @RequiresPermissions("entertainment:diningentertainment:list")
    @GetMapping("/list")
    public TableDataInfo list(Diningentertainment diningentertainment)
    {
        startPage();
        List<Diningentertainment> list = diningentertainmentService.selectDiningentertainmentList(diningentertainment);
        return getDataTable(list);
    }

    /**
     * 导出餐饮娱乐信息列表
     */
    @RequiresPermissions("entertainment:diningentertainment:export")
    @Log(title = "餐饮娱乐信息", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, Diningentertainment diningentertainment)
    {
        List<Diningentertainment> list = diningentertainmentService.selectDiningentertainmentList(diningentertainment);
        ExcelUtil<Diningentertainment> util = new ExcelUtil<Diningentertainment>(Diningentertainment.class);
        util.exportExcel(response, list, "餐饮娱乐信息数据");
    }

    /**
     * 获取餐饮娱乐信息详细信息
     */
    @RequiresPermissions("entertainment:diningentertainment:query")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(diningentertainmentService.selectDiningentertainmentById(id));
    }

    /**
     * 新增餐饮娱乐信息
     */
    @RequiresPermissions("entertainment:diningentertainment:add")
    @Log(title = "餐饮娱乐信息", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody Diningentertainment diningentertainment)
    {
        return toAjax(diningentertainmentService.insertDiningentertainment(diningentertainment));
    }

    /**
     * 修改餐饮娱乐信息
     */
    @RequiresPermissions("entertainment:diningentertainment:edit")
    @Log(title = "餐饮娱乐信息", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody Diningentertainment diningentertainment)
    {
        return toAjax(diningentertainmentService.updateDiningentertainment(diningentertainment));
    }

    /**
     * 删除餐饮娱乐信息
     */
    @RequiresPermissions("entertainment:diningentertainment:remove")
    @Log(title = "餐饮娱乐信息", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(diningentertainmentService.deleteDiningentertainmentByIds(ids));
    }
}
